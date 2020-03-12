import requests
import re
import os
import threading

test_address = ''


def run_crawler(deep, url):
    # Core function in whole program
    # Used to get the list of href list and save the images
    deep = 5
    webpage = get_html(url)

    image_list, hyper_list = get_required_hrefs(webpage)

    if image_list:
        for i in image_list:
            print("List img links")
            print(i)
            img_url, file_name, folder_path = get_image_components(i, url)
            content = download_image(img_url, file_name, folder_path)
            if content != '':
                save_image(folder_path, content, file_name)
            else:
                pass

    if hyper_list:
        for v in hyper_list:
            print("List hyperlinks")
            if v.split('/')[-1] not in url:  # Avoid to back to the previous url
                hyper = url + '/' + v.split('/')[-1]
                print(hyper)
                run_crawler(deep, hyper)

    # End the program when both lists are empty
    if len(image_list) == 0:
        if len(hyper_list) == 0:
            return ''


def get_image_components(img_link, previous_url):
    # Obtain important components for image download
    img_url = previous_url + '/'+img_link.split('/')[-1]
    file_name = img_link.split('/')[-1]
    folder_path = previous_url
    return img_url, file_name, folder_path


def download_image(url, file_name, folder_path):
    # Download the images by connecting to the URL of image
    print("list all the tags of images: ")
    try:
        r = requests.get(url, timeout=1)
        print(r.status_code)
        result = test_status_code(str(r.status_code))
        if result is True:
            content = r.content
            # Return the pic content which used to be save image
            return content
        else:
            return ''
    except Exception as e:
        print(e)


def save_image(path, content, file_name):
    # Save image in the local
    address = make_folder(path)
    with open(address+'/'+file_name, 'wb') as f:
        f.write(content)
        f.close()
        print('save')


def make_folder(folder_path):
    # Create relevant folder for group images with different depths
    # Avoid the redundancy of the folders
    folder_path = folder_path.split('//')[1]
    if os.path.exists(folder_path):
        return folder_path
    else:
        os.makedirs(folder_path)
        return folder_path


def test_status_code(code):
    # Test the validity of the web connection
    if code.startswith('2'):
        print("Good connection")
        return True
    else:
        print("Disabled connection")
        return False


def get_html(url):
    # Analyze and return the content of input url
    global test_address
    try:
        r = requests.get(url, timeout=1)
        html = r.text.encode()
        print(r.status_code)
        result = test_status_code(str(r.status_code))
        if result is True:
            if url == test_address:
                # Only save the html content of the input URL as the file for checking
                path = url.replace('/', ' ') + '.html'
                with open(path, 'wb') as f:
                    f.write(html)
                    f.close()
                print('Done')
            else:
                pass
            return r.content.decode('utf-8') # Use utf-8 to decode the content in Chinese pattern
        else:
            print("Error connection")
            return ''
    except Exception as e:
        print(e)


def get_required_hrefs(html):
    # Use Regular Expression to extract the image and hyper links in HTML content
    result_pic = re.findall(r'<img\ssrc="(.*?)"/>', html)

    result_hyper = re.findall(r'<a.*?href\s*=\s*"(.*?)".*?>', html)

    return result_pic, result_hyper


def get_input():
    # Get input from user
    test_address = input('Please enter valid url\n')
    # Unfortunately, with multiple tries, so far only
    # http://www.feimax.com/images could be successfully used to do image crawler
    deep = input('Please enter depth for iteration\n')

    return test_address, deep


def main():
    #test_address, deep = get_input()
    default_test_address = 'http://www.feimax.com/images'
    default_deep = 5
    run_crawler(default_deep, default_test_address)


if __name__ == '__main__':
    main()
    # End of the whole program
    print("Image crawler has ended.")






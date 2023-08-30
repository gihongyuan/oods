import hashlib
import json

import requests
from django.shortcuts import render

import browser.constant as constant


def index(request):
    # 提取页面参数
    params = request.GET

    # 构造编辑器参数
    context = {
        'apiUrl': get_oods_server(request) + constant.DOC_SERV_API_URL,
        'editorConfig': json.dumps(get_editor_config(params)),
    }
    print(f'Get editor config success: {context}')

    return render(request, "editor.html", context)


def get_query(params, key, default=None, allow_empty=False, error_message=None):
    # 提取接口参数
    value = params.get(key, default)

    # 不允许参数为空时，如果参数为空，则抛出异常
    if not value and not allow_empty:
        raise ValueError(error_message or "Missing parameter '%s'" % key)

    return value


def get_oods_server(request):
    oods_host = request.META.get('REMOTE_ADDR')

    # 判断是否为https请求
    is_https = request.is_secure()
    protocol = 'https' if is_https else 'http'
    oods_port = constant.HTTPS_OODS_PORT if is_https else constant.HTTP_OODS_PORT

    # 优先使用oods参数中的地址，否则使用当前请求地址
    oods_server = request.GET.get(constant.DOCUMENT_SERVER_FIELD, f"{protocol}://{oods_host}:{oods_port}/")
    return oods_server


def get_editor_config(params):
    def get_document_type(file_type):
        if file_type in constant.DOC_CELL_LIST:
            return 'cell'
        elif file_type in constant.DOC_SLIDE_LIST:
            return 'slide'
        else:
            return 'word'

    # 获取文件信息
    title, fileType, fileId, fileUrl, fileKey = get_file_info(params)

    return {
        'document': {
            'fileType': fileType,
            'key': fileKey,
            'title': title,
            'url': fileUrl,
            'permissions': {
                'chat': False,
                'comment': False,
                'download': False,
                'print': False,
            }
        },
        'documentType': get_document_type(fileType),
        'editorConfig': {
            'mode': 'view',
            'lang': get_query(params, constant.LANGUAGE_FIELD, default=constant.DEFAULT_LANGUAGE),
            'customization': {
                'anonymous': {
                    'request': False,
                },
                'plugins': False,
                'help': False,
            }
        }
    }


def get_file_info(params):
    def get_file_key(file_sha256):
        return hashlib.sha256(file_sha256.encode()).hexdigest() if file_sha256 else None

    # 获取文件服务器地址
    file_server = get_query(params, constant.FILE_SERVER_FIELD, error_message='FileServer Host is required!')

    # 获取文件接口路径及文件ID
    file_info_api = get_query(params, constant.FILE_INFO_API_FIELD, default=constant.DEFAULT_FILE_INFO_API)
    file_get_api = get_query(params, constant.FILE_DOWNLOAD_API_FIELD, default=constant.DEFAULT_FILE_DOWNLOAD_API)
    file_id = get_query(params, constant.FILE_ID_FIELD, error_message='FileId is required!')

    # 调用接口获取文件信息
    try:
        response = requests.get(file_server + file_info_api, params={constant.FILE_ID_FIELD: file_id})
        response.raise_for_status()
        file_info = response.json()
    except requests.exceptions.HTTPError as e:
        raise ValueError(f"FileServer API Error: {e}")

    # 提取有效信息
    file_name = file_info.get('BaseFileName')
    file_suffix = file_name.split('.')[-1].lower()
    file_url = f'{file_server}{file_get_api}?{constant.FILE_ID_FIELD}={file_id}'
    file_key = get_file_key(file_info.get("SHA256"))

    # 返回文件名及文件类型
    return file_name, file_suffix, file_id, file_url, file_key

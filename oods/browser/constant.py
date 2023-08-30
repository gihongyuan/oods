# 文档类型分类列表
import os

DOC_WORD_LIST = ["doc", "docm", "docx", "docxf", "dot", "dotm", "dotx", "epub", "fodt", "fb2", "htm", "html",
                 "mht", "odt", "oform", "ott", "oxps", "pdf", "rtf", "txt", "djvu", "xml", "xps"]
DOC_CELL_LIST = ["csv", "fods", "ods", "ots", "xls", "xlsm", "xlsx", "xlsb", "xlt", "xltm", "xltx"]
DOC_SLIDE_LIST = ["fodp", "odp", "otp", "pot", "potm", "potx", "pps", "ppsm", "ppsx", "ppt", "pptm", "pptx"]

# onlyoffice文档服务api路径
DOC_SERV_API_URL = 'web-apps/apps/api/documents/api.js'

# 默认参数字段
LANGUAGE_FIELD = 'lang'
FILE_SERVER_FIELD = 'host'
DOCUMENT_SERVER_FIELD = 'oods'
FILE_ID_FIELD = 'fileId'
FILE_INFO_API_FIELD = 'getFileInfo'
FILE_DOWNLOAD_API_FIELD = 'downloadFile'
HTTP_OODS_PORT_FIELD = 'HTTP_OODS_PORT'
HTTPS_OODS_PORT_FIELD = 'HTTPS_OODS_PORT'

# 默认参数值
DEFAULT_LANGUAGE = 'zh'
DEFAULT_FILE_INFO_API = "/api/file/info"
DEFAULT_FILE_DOWNLOAD_API = "/api/file/download"
HTTP_OODS_PORT = os.getenv(HTTP_OODS_PORT_FIELD) or 80
HTTPS_OODS_PORT = os.getenv(HTTPS_OODS_PORT_FIELD) or 443

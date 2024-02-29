from oauth2client.service_account import ServiceAccountCredentials
import apiclient
import httplib2
from config import SERVICE_ACC_INFO


def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

    Args:
        element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get("textRun")
    if not text_run:
        return ""
    return text_run.get("content")


def read_structural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
    in nested elements.

    Args:
        elements: a list of Structural Elements.
    """
    text = ""
    for value in elements:
        if "paragraph" in value:
            elements = value.get("paragraph").get("elements")
            for elem in elements:
                text += read_paragraph_element(elem)
        elif "table" in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get("table")
            for row in table.get("tableRows"):
                cells = row.get("tableCells")
                for cell in cells:
                    text += read_structural_elements(cell.get("content"))
        elif "tableOfContents" in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get("tableOfContents")
            text += read_structural_elements(toc.get("content"))
    return text


def get_doc(url: str):
    url = url.split("/")[5]
    print(url)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        SERVICE_ACC_INFO,
        [
            "https://www.googleapis.com/auth/docs",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build("docs", "v1", http=httpAuth)
    doc = service.documents().get(documentId=url).execute()
    doc_content = doc.get("body").get("content")
    return read_structural_elements(doc_content)


def get_spreadsheet_id(url: str):

    url = url.split("/")[5]

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        SERVICE_ACC_INFO,
        [
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build("drive", "v3", http=httpAuth)
    doc = service.files().get_media(fileId=url)
    try:
        doc = doc.execute().decode("utf-8")
    except Exception as e:
        print(e)
        return 0

    return doc.split("/")[5]

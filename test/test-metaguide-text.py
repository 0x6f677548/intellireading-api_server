if __name__ == "__main__":
    from transforming.metaguiding.regex import RegExBoldMetaguider

    with open("/mnt/c/code/projects/intellireading/test/document_file1.1.xhtml", "rb") as f_:
        _file_content = f_.read()

    _metaguider = RegExBoldMetaguider()
    result = _metaguider.metaguide_xhtml_document(_file_content)
    print(result)

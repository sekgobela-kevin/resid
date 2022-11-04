# resid

### Description
**Resid** is a python library for analysing resource identifiers 
for extracting valuable information. This can include guessing content 
type, encoding, checking if contents are available locally or if it 
resembles file path, url, etc.

In this library, _source_ is defined as similar to _uri_ but source
can be anything including file object. 'source' is defined as anything
that can be used to access/locate contents. That can include _url_, 
_file path_, _file object_ and others depending on whether
they can be used to access data or get information about it.

Any object can be used as source but not all of them will be supported.
This library helps in extracting information about source such as whether
source is supported or guessing its content type.

### Install
Enter this on your command-line application:  
```bash 
pip install resid
```
> resid -> Resource Identifier

### Usage
Supported source is source that is guaranteed to be supported while 
resembled source is not guaranteed.
```python
>>> import resid
>>>
>>> resid.is_supported("https://stackoverflow.com/")
True
>>> resid.is_supported("not_exists.txt")
False
>>> resid.is_resembled("not_exists.txt")
True
>>> resid.is_supported(io.BytesIO())
True
>>> resid.is_resembled(object)
False
```

Source can be checked to see if its url, file path, etc using few 
functions which may return None if source is not supported.
```python
>>> resid.is_url("https://example.com/")
True
>>> resid.is_web_url("https://example.com/")
True
>>> resid.is_file_path("https://example.com/")
False
>>> resid.is_file_path("sample.txt")
True
>>> resid.is_file_path(object)
False
>>> resid.is_file_like(io.BytesIO())
True
>>> resid.is_path_like(pathlib.Path("sample.txt"))
True
```

Content type of source can be guessed from source itself especially 
file paths and urls for webpages.
```python
>>> resid.guess_content_type("sample.txt")
'text/plain'
>>> resid.guess_content_type("https://example.com/")
'text/html'
>>> resid.guess_content_type("https://example.com/files/sample.pdf")
'application/pdf'
>>> resid.guess_content_type(open("sample.txt"))
'text/plain'
```

It may be important to know if source contents are hosted locally 
or remotely if intending to fetch contents.
```python
>>> resid.locally_hosted("sample.txt")
True
>>> resid.locally_hosted("https://example.com/")
False
>>> resid.locally_hosted("http://127.0.0.1/")
True
>>> resid.guess_content_type(open("sample.txt"))
True
>>> resid.remotely_hosted("sample.txt")
False
>>> resid.remotely_hosted("https://example.com/")
True
>>> resid.remotely_hosted("file:///home/sample.txt")
False
```

String version of source can be created from path part source if exists.
```python
>>> resid.to_string(open("setup.py"))
'setup.py'
>>> resid.to_string(pathlib.Path("sample.txt"))
'sample.txt'
>>> resid.to_string("https://example.com/")
'https://example.com/'
```


More extensions, content types and encodings can be added through 
`mimetypes`
module.
```python
>>> import mimetypes
>>>
>>> mimetypes.common_types[".jpg"] = "image/jpg"
>>> mimetypes.encodings_map[".gz"] = "gzip" 
```

### License
[MIT license](https://github.com/sekgobela-kevin/resid/blob/main/LICENSE)
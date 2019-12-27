# home-iot-automation
Different things that work in the background to help me getting things done or notify me or ...

## Workflow steps

1. File Watcher - Notify other services about new files
2. Page Detector - Remove blank pages and rotate pages
3. OCR Service - Do OCR on every single file
4. Document Creator - Merge pages that belongs together
5. Archiver - Move the final file to the destination path and archiv encrypted copies of the raw scan file and the final PDF to a cloud service for backup purposes
6. Notification Service - Notify the user about successful processing of all previous steps so he can shred the papers.

### Restrictions

* Files should never be removed from its source.

## Protocol

### File Watcher

*Output Topic*: scan_new_file
The topic is used to notify services, that do like to process the file, about new files.
This could be logging services or archiving services and the Page Detector.
The data send to the topic will look like this.

```json
{
  file_path: '/absolute/path/to/the/scanned/image/{original_filename_with_extension}'
}
```


### Page Detector

The Page Detector will read from the `scan_new_file` topic and drops blank pages or rotates non-blank pages.
It outputs a new file and it's path to another topic with the data shown below.

*Output Topic*: scan_new_prepared_file

```json
{
  file_path: '/absolute/path/to/the/prepared/image/{YYYY-MM-DD}_{original_filenam_with_extension}'
}
```


### OCR Service

The OCR Service will read from the `scan_new_prepared_file` topic and does the OCR on the file given.
The output will be a PDF file with searchable text of the scanned image included. 
The output file path will be published to a new topic.

*Output Topic*: scan_new_pdf_page

```json
{
  file_path: '/absolute/path/to/the/pdf/page/{YYYY-MM-DD}_{original_filename}.pdf'
}
```

### Document Creator 

The Document Creator will merge PDF pages that belongs together.
This does rely heavily (currently only) on the filename suffix `*_0001.pdf` which does represent the page numbers.

*Output Topipc*: scan_new_pdf

```json
{
  file_path: '/absolute/path/to/the/pdf/{YYYY-MM-DD}_{original_filename_without_pages_suffix}.pdf'
}
```

## TODO

* The scan reader should check multiple folders.

# Ofis & Belge

Word/PowerPoint/Excel/PDF üretimi ve düzenlemesi (Anthropic yerleşik).

4 skill. Üst dizin: [../../README.md](../../README.md)

## `docx`

[SKILL.md](docx/SKILL.md)

Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx) or Word templates (.dotx). Triggers include: any mention of 'Word doc', 'word document', '.docx', '.dotx', or requests to produce professional documents with formatting like tables of contents, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx or .dotx files, inserting or replacing images in documents, find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file (to download, email or print), use this skill. However, if they ask for a document, page, report, memo, or notes WITHOUT naming a file format and the session offers a dedicated document or page skill or connector, use that instead. Do NOT use for PDFs, spreadsheets, Google Docs, or coding unrelated to document generation.

- **Ölçü:** 7.036 bayt · 60 ek dosya · script içerir
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `pdf`

[SKILL.md](pdf/SKILL.md)

Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.

- **Ölçü:** 8.035 bayt · 11 ek dosya · script içerir
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `pptx`

[SKILL.md](pptx/SKILL.md)

Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations as PowerPoint (.pptx) files; reading, parsing, or extracting text from any .pptx or .potx file (even if the extracted content will be used elsewhere, like in an email, summary, or creating a different type of slide deck); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates (.potx), layouts, speaker notes, or comments. Trigger whenever the user asks for a PowerPoint or .pptx file, or references a .pptx or .potx filename, regardless of what they plan to do with the content afterward. However, when the user asks for a deck, slides, a slide deck, or a presentation without naming a file format, default to using a dedicated slide-deck artifact type or a separate slides skill if this session offers one; otherwise, use this skill.

- **Ölçü:** 21.423 bayt · 55 ek dosya · script içerir
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `xlsx`

[SKILL.md](xlsx/SKILL.md)

Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .xltx, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.

- **Ölçü:** 8.542 bayt · 52 ek dosya · script içerir
- **Kaynak:** claude.ai senkronu (efemer önbellek)


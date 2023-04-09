# All-Things-Makefile-File
#

Md-File-List = $(wildcard *.md)
Html-File-List = $(subst .md,.html,$(Md-File-List)) index.html

define Markdown_to_Html
	pandoc --standalone --template 300000002.htm $(1) -o $(2)
	sed -i '' -E 's/(href="[0-9]+)\.md/\1\.html/g' $(2)
endef

all: Html-Files
	echo "All-Things-Makefile-File"

Html-Files: $(Html-File-List)

## Web-Server-Directory-Index-Rule

index.html: .github/Readme.md
	$(call Markdown_to_Html, $<, $@)

%.html: %.md
	$(call Markdown_to_Html, $<, $@)

clean:
	rm -f $(Html-File-List)

.PHONY: all clean

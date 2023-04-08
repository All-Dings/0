# # All-Things-Makefile-File
#

Md-File-List = $(wildcard *.md)
Html-File-List = $(subst .md,.html,$(Md-File-List))

all: Html-Files
	echo "All-Things-Makefile-File"

Html-Files: $(Html-File-List)

%.html: %.md
	pandoc --standalone --template 300000002.htm $< -o $@
	sed -i '' -E 's/(href="[0-9]+)\.md/\1\.html/g' $@

clean:
	rm -f $(Html-File-List)

.PHONY: all clean

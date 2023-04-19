# All-Things-Makefile-File
#

Md-File-List = $(wildcard *.md)
Html-File-List := $(subst .md,.html,$(Md-File-List)) index.html
Html-File-List := $(addprefix ${DINGS_DAY}/, $(Html-File-List))

define Markdown_to_Html
	pandoc --standalone --template 300000002.htm $(1) -o $(2)
	sed -i '' -E 's/(href="[0-9]+)\.md/\1\.html/g' $(2)
	sed -i '' -E 's#<body>#<body><pre class="console"><code>Warning: Although I give my very Best, Mistakes are still possible.</code></pre>#g' $(2)
endef

all: Html-Files
	echo "All-Things-Make-File:${DINGS_DAY}"

Html-Files: $(Html-File-List)

## Web-Server-Directory-Index-Rule

${DINGS_DAY}/index.html: 300000006.md
	$(call Markdown_to_Html, $<, $@)

${DINGS_DAY}/%.html: %.md
	$(call Markdown_to_Html, $<, $@)

clean:
	rm -f $(Html-File-List)

.PHONY: all clean

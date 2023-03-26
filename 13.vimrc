"
"# Clash of Clans vimrc File
"

"## Find Name in Number Files

func! FindName()
	" Get Word under Cursor:
	let Name = expand("<cword>")
	" Construct the bash command
	let Cmd = "head -n 1 *.md | grep -B 1 " . Name
	" Call Command and print Output to Console
	echo system(Cmd)
endfunc

"## Map FindName to Key 'f' in Normal Mode

nnoremap f :call FindName()<CR>

"## Whitespace Highlighting

highlight ExtraWhitespace ctermbg=red guibg=red
match ExtraWhitespace /\s\+$/

"## Attribution
"
"- https://stackoverflow.com/questions/4617059/showing-trailing-spaces-in-vim

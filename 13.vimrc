"
" # Clash of Clans vimrc File
"

" ## Find Name in Number Files

func! FindName()
	" Get Word under Cursor:
	let Name = expand("<cword>")
	" Construct the bash command
	let Cmd = "head -n 1 *.md | grep -B 1 " . Name
	" Call Command and print Output to Console
	echo system(Cmd)
endfunc

" ## Map FindName to Key 'f' in Normal Mode

nnoremap f :call FindName()<CR>

" ## Whitespace Highlighting
"
" - https://stackoverflow.com/questions/4617059/showing-trailing-spaces-in-vim
"
highlight ExtraWhitespace ctermbg=red guibg=red
match ExtraWhitespace /\s\+$/

syntax on

" ## To-Dos
"
" ### Highlight trailing Blans
"
" highlight LeadingBlanks ctermbg=red guibg=red
" match LeadingBlanks /^[ ]\+/
"
" ### Show leading Tabs
"
" - https://medium.com/usevim/understanding-listchars-acb9e5a90854
"
set list
set listchars=tab:>-,trail:~,extends:>,precedes:<

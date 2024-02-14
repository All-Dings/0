# # Bash Configruation File

# ## Bash Completion
#
# Prequisite: ```$ apt-get install git bash-completion```
source /opt/homebrew/etc/bash_completion.d/hub.bash_completion.sh

# ## Find Name in Number Files
alias mms="head -n 1 *.md | grep -i -B 1 "

if [ -f "$(brew --prefix)/opt/bash-git-prompt/share/gitprompt.sh" ]; then
	__GIT_PROMPT_DIR=$(brew --prefix)/opt/bash-git-prompt/share
	GIT_PROMPT_ONLY_IN_REPO=1
	source "$(brew --prefix)/opt/bash-git-prompt/share/gitprompt.sh"
fi

# ## Prompt Setup
#
# - __git_ps1: Git Prompt that shows current Branch
# - \[\e[0;32m\]: green
# - \[\e[0;31m\]: red
# - \[\e[0;32m\]: green
# - \[\e[m]: End color mode
# PS1='\[\e[0;32m\]\u:\w$(__git_ps1 " \[\e[0;31m\](%s)")\[\e[0;32m\]\$ \[\e[m\]'
PS1='\[\e[0;32m\]\u:\w\[\e[0;32m\]\$ \[\e[m\]'

# ## Enable Colors for Files and Directories
alias ls="ls --color=auto"

# # Ask before overwriting
#
# ## References
#
# - [Better safe than sorry](
alias mv="mv -i"

# Bash Completion (Not completed)
Dings_Completion()
{
	echo "Input: \"${COMP_WORDS[1]}\" \"${COMP_WORDS[2]}\" \"${COMP_WORDS[3]}\"" >> out
	echo "Cword: ${COMP_CWORD}" >> out
	out=$(./dings completion ${COMP_WORDS[1]} ${COMP_WORDS[2]} ${COMP_WORDS[3]} -p ${COMP_CWORD})
	echo "Tool: \"$out\"" >> out
	COMPREPLY=$(./dings completion ${COMP_WORDS[1]} ${COMP_WORDS[2]} ${COMP_WORDS[3]} -p ${COMP_CWORD})
}

# ## Node.js

export NVM_DIR=~/.nvm
source $(brew --prefix nvm)/nvm.sh

# ## Dings-System
complete -F Dings_Completion dings

export Dings_Big_Data_Directory="Tbd"
export Dings_Big_Data_Url="Tbd"
export Dings_Work_Directory="Tbd"
export PATH=$PATH:/opt/homebrew/bin/
export PATH=$PATH:.:$Dings_Work_Directory

# # Bash Configruation File

# ## Bash Completion
#
# Prequisite: ```$ apt-get install git bash-completion```
source /etc/profile.d/bash_completion.sh

# ## Find Name in Number Files
alias mms="head -n 1 *.md | grep -i -B 1 "

# ## Prompt Setup
#
# - __git_ps1: Git Prompt that shows current Branch
# - \[\e[0;32m\]: green
# - \[\e[0;31m\]: red
# - \[\e[0;32m\]: green
# - \[\e[m]: End color mode
PS1='\[\e[0;32m\]\u:\w$(__git_ps1 " \[\e[0;31m\](%s)")\[\e[0;32m\]\$ \[\e[m\]'

# ## Enable Colors for Files and Directories
eval "$(dircolors -b)"
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

complete -F Dings_Completion dings

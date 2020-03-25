SHELL_SESSION_HISTORY=0

HISTSIZE=10000
HISTFILESIZE=20000
shopt -s histappend

HISTCONTROL=ignoreboth

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias bb='screen -dmSL $(openssl rand -hex 12)'
alias dus='du -shc .??* *'


export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

#HOME BIN PATH
export PATH=$PATH:$HOME/bin

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

#HOMEBREW INSTALL PATH
export PATH=$PATH:/usr/local/sbin

mktouch() {
    if [ $# -lt 1 ]; then
        echo "Missing argument";
        return 1;
    fi

    for f in "$@"; do
        mkdir -p -- "$(dirname -- "$f")"
        touch -- "$f"
    done
}

export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
launchctl setenv OBJC_DISABLE_INITIALIZE_FORK_SAFETY YES


export GITAWAREPROMPT=~/.bash/git-aware-prompt
source "${GITAWAREPROMPT}/main.sh"

if [ -f $(brew --prefix)/etc/bash_completion ]; then
  . $(brew --prefix)/etc/bash_completion
fi

if [ -f ~/.bash/git-completion.bash ]; then
  . ~/.bash/git-completion.bash
fi

#SSH AGENT
ls $HOME/.ssh/ | grep "id_rsa$" | xargs -I {} ssh-add $HOME/.ssh/{}

set nocompatible              " required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'
Plugin 'kien/ctrlp.vim'
Plugin 'tpope/vim-fugitive'
Plugin 'nvie/vim-flake8'
Plugin 'scrooloose/nerdcommenter'
Plugin 'ervandew/supertab'


" you complete me
autocmd FileType vim let b:vcm_tab_complete = 'vim'


" Add all your plugins here (note older versions of Vundle used Bundle instead of Plugin)


" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required

set number
set laststatus=2
set ignorecase
set showmatch
set copyindent
set hlsearch
set ruler
set smarttab
set smartcase
set nowrap
set showcmd
syntax on
set autoindent
filetype plugin indent on
set nocompatible
set incsearch
set history=10000

"Return to last edit position when opening files
autocmd BufReadPost *
     \ if line("'\"") > 0 && line("'\"") <= line("$") |
     \   exe "normal! g`\"" |
     \ endif 

autocmd BufEnter * silent! lcd %:p:h
set autoread
set title
set cc=80,120,160

"tabs
"
set ts=2
set et
set sw=2
set shiftwidth=2 
set softtabstop=2
set tabstop=2
set expandtab

vnoremap < <gv
vnoremap > >gv
vnoremap // y/<C-R>"<CR>

if exists("+undofile")
  " undofile - This allows you to use undos after exiting and restarting
  " This, like swap and backups, uses .vim-undo first, then ~/.vim/undo
  " :help undo-persistence
  " This is only present in 7.3+
  if isdirectory($HOME . '/.vim/undo') == 0
    :silent !mkdir -p ~/.vim/undo > /dev/null 2>&1
  endif
  set undodir=./.vim-undo//
  set undodir+=~/.vim/undo//
  set undofile
endif

function! SuperTab()
    if (strpart(getline('.'),col('.')-2,1)=~'^\W\?$')
        return "\<Tab>"
    else
        return "\<C-n>"
    endif
endfunction
autocmd BufWritePost *.py call Flake8()
set mouse=niv
set runtimepath^=~/.vim/bundle/ctrlp.vim
set backspace=indent,eol,start
autocmd filetype crontab setlocal nobackup nowritebackup
set runtimepath^=~/.vim/bundle/vim-erlang-runtime/

"stop indent when copy-paste
let &t_SI .= "\<Esc>[?2004h"
let &t_EI .= "\<Esc>[?2004l"

inoremap <special> <expr> <Esc>[200~ XTermPasteBegin()

function! XTermPasteBegin()
  set pastetoggle=<Esc>[201~
  set paste
  return ""
endfunction
let &t_SI .= "\<Esc>[?2004h"
let &t_EI .= "\<Esc>[?2004l"

let g:syntastic_cpp_compiler = 'clang++'
let g:syntastic_cpp_compiler_options = ' -std=c++11 -stdlib=libc++'
let g:ctrlp_by_filename = 1
autocmd BufWritePost *.py call flake8#Flake8()


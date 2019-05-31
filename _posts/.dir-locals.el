;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((gfm-mode .
           ((eval remove-hook 'before-save-hook 'markdownfmt-format-buffer t))))

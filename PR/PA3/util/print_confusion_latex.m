function [ ] = print_confusion_latex( confusion )
     % Do confusion latex
    n_classes = length(confusion);
    printf('\n\\begin{tabular}{ | l | ');
    for i=1:n_classes
        printf('c | ');
    end
    printf('}\n\\hline\n');
    
    for i=1:n_classes
        printf('& $\\omega_%d$ ', i);
    end
    printf('\\\\\n');
    
    for i=1:n_classes
        printf('\\hline\n');
        printf('  $\\omega_%d$ ', i);
        for j=1:n_classes
            printf('& %d ', confusion(i,j))
        end
        printf('\\\\\n');
    end
    
    printf('\\hline\n');
    printf('\\end{tabular}\n');

%{
\begin{tabular}{ l | c | c | c | }

& $\omega_1$ & $\omega_2$ & $\omega_3$ \\
\hline
  $\omega_1$ & 124 & 1 & 0 \\ 
\hline
  $\omega_2$ & 0 & 125 & 0 \\
\hline
  $\omega_3$ & 0 & 0 & 125 \\
\hline
\end{tabular}  
%}


end


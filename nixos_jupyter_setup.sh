nix-shell -p 'python3.withPackages(ps: with ps; [ numpy jupyter sympy])' nodejs

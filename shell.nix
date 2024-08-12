let
	pkgs = import <nixpkgs> {};
in pkgs.mkShell {
	packages = [
		(pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
			requests
			beautifulsoup4
			requests-cache
		]))
		pkgs.clang-tools
	];
}

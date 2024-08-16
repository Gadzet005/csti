let
	pkgs = import <nixpkgs> {};
in pkgs.mkShell {
	packages = [
		(pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
			requests
			beautifulsoup4
			requests-cache
			click
			inquirerpy
			platformdirs
			pyyaml
		]))
		pkgs.clang-tools
	];
}

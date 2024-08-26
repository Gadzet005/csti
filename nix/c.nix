let
	pkgs = import <nixpkgs> {};
in pkgs.mkShell {
	packages = [
		pkgs.clang-tools
        pkgs.libgcc
	];
}
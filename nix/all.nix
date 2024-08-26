let
	pkgs = import <nixpkgs> {};
in pkgs.mkShell {
	packages = [
		pkgs.clang-tools
        pkgs.libgcc
	];
	nativeBuildInputs = with pkgs.buildPackages; [
		pkgsi686Linux.gcc
		pkgsi686Linux.nasm
	];
}
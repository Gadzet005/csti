let
	pkgs = import <nixpkgs> {};
in pkgs.mkShell {
	nativeBuildInputs = with pkgs.buildPackages; [
		pkgsi686Linux.gcc
		pkgsi686Linux.nasm
  	];
}
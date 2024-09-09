{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";

    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs@{ self, poetry2nix, ... }:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ ./nix/templates.nix ];

      systems =
        [ "x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];

      perSystem = { pkgs, system, ... }: {
        packages = let
          inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; })
            mkPoetryApplication;
        in {
          csti = mkPoetryApplication { projectDir = self; };
          default = self.packages.${system}.csti;
        };

        devShells = let
          inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryEnv;
        in {
          default = pkgs.mkShellNoCC {
            packages = with pkgs; [
              (mkPoetryEnv { projectDir = self; })
              poetry
            ];
          };

          nix-shell = pkgs.mkShellNoCC {
            packages = with pkgs; [ nixfmt-classic deadnix statix ];
          };

          tests = pkgs.mkShellNoCC {
            packages = with pkgs; [
              (mkPoetryEnv { projectDir = self; })
              poetry
              cmake
              gcc
              clang-tools
            ];
          };
        };
      };
    };
}

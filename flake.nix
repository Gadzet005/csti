{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";

    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs@{ self, nixpkgs, poetry2nix, ... }:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } {
      systems =
        [ "x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];

      perSystem = { self', inputs', pkgs, system, config, ... }: {
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

              nixfmt
            ];

            shellHook = ''
              exec fish;
            '';
          };
        };
      };

      flake = { 
        templates = rec {
          # TODO: Актуализировать команды.
          default = {
            path = ./nix/shell_templates/default;
            description = "Empty template with csti.";
            welcomeText = ''
              # Getting started
              - Run `nix develop`
              - Run `csti configure`
            '';
          };
          c = {
            path = ./nix/shell_templates/c;
          };
          cpp = {
            path = ./nix/shell_templates/cpp;
          };
          nasm = {
            path = ./nix/shell_templates/nasm;
          };
        };
      };
    };
}

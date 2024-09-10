{
  description = "Basic csti flake.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    csti.url = "github:Gadzet005/csti";
  };

  outputs =
    { nixpkgs, ... }@inputs:
    let
      supportedSystems = [
        "x86_64-linux"
        "x86_64-darwin"
        "aarch64-linux"
        "aarch64-darwin"
      ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgs = forAllSystems (system: nixpkgs.legacyPackages.${system});

    in
    {
      devShells = forAllSystems (system: {
        default = pkgs.${system}.mkShellNoCC {
          packages = with pkgs.${system}; [
            #	Добавьте необходимые вам пакеты(их названия можно найти на
            # сайте https://mynixos.com).

            inputs.csti.packages.${system}.default
          ];

          # Вместо shell подставьте вашу оболочку командной строки и
          # расскоментируйте строку.
          shellHook = ''
            # exec shell
          '';
        };
      });
    };
}

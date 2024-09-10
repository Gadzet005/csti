{ self, inputs, ... }:
{
  perSystem =
    { pkgs, system, ... }:
    {
      devShells =
        let
          inherit (inputs.poetry2nix.lib.mkPoetry2Nix { inherit pkgs; })
            mkPoetryEnv
            ;
        in
        {
          default = pkgs.mkShellNoCC {
            packages = with pkgs; [
              (mkPoetryEnv { projectDir = self; })
              poetry
            ];
          };

          tests = pkgs.mkShellNoCC {
            # TODO: При большом пересечении пакетов брать шелы из templates.
            packages = with pkgs; [
              cmake
              gcc
              clang-tools
            ];
            inputsFrom = [ self.devShells.${system}.default ];
          };
        };
    };
}

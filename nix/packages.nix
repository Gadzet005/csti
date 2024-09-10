{ self, inputs, ... }:
{
  perSystem =
    { pkgs, system, ... }:
    {
      packages =
        let
          inherit (inputs.poetry2nix.lib.mkPoetry2Nix { inherit pkgs; })
            mkPoetryApplication
            ;
        in
        {
          csti = mkPoetryApplication { projectDir = self; };
          default = self.packages.${system}.csti;
        };
    };
}

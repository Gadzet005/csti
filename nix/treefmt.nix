_: {
  perSystem =
    { config, ... }:
    {
      treefmt.config = {
        projectRootFile = "flake.nix";

        programs = {
          # Python.
          black.enable = true;
          isort.enable = true;

          # Nix.
          deadnix.enable = true;
          statix.enable = true;
          nixfmt.enable = true;
        };
      };
    };
}

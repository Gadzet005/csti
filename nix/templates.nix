_:

{
  flake.templates = rec {
    # TODO: Актуализировать команды.
    default = {
      path = ./shell_templates/default;
      description = "Empty template with csti.";
      welcomeText = ''
        # Getting started
        - Run `nix develop`
        - Run `csti configure -g`
      '';
    };
    c-template = {
      path = ./shell_templates/default;
      description = "Template for C csti.";
      welcomeText = ''
        # Getting started
        - Run `nix develop`
        - Run `csti configure -g`
      '';
    };
  };
}

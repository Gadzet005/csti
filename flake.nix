{
	inputs = {
		nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
		poetry2nix = {
			url = "github:nix-community/poetry2nix";
			inputs.nixpkgs.follows = "nixpkgs";
		};
	};

	outputs = { self, nixpkgs, poetry2nix }: let
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
		packages = forAllSystems (system: let
			inherit (poetry2nix.lib.mkPoetry2Nix { pkgs = pkgs.${system}; }) mkPoetryApplication;
		
		in {
			csti = mkPoetryApplication { projectDir = self; };
			default = self.packages.${system}.csti;
		});

		devShells = forAllSystems (system: let
			inherit (poetry2nix.lib.mkPoetry2Nix { pkgs = pkgs.${system}; }) mkPoetryEnv;
		
		in {
			default = pkgs.${system}.mkShellNoCC {
				shellHook = ''
					exec $SHELL 
				'';
				packages = with pkgs.${system}; [
					(mkPoetryEnv { projectDir = self; })
					poetry
				];
			};
		});
	};
}

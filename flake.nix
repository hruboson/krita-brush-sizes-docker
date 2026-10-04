{
  description = "Krita plugin for docker with predefined brush sizes";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];
      forAll = f: nixpkgs.lib.genAttrs systems (s: f nixpkgs.legacyPackages.${s});
    in
    {
      # Installable plugin: $out/share/krita/pykrita/{brush-sizes-docker.desktop,brush-sizes-docker/}
      packages = forAll (pkgs: {
        default = pkgs.stdenvNoCC.mkDerivation {
          pname = "krita-plugin-brush-sizes-docker";
          version = "0.0.1";
          src = ./.;
          dontBuild = true;
          installPhase = ''
            dest=$out/share/krita/pykrita
            mkdir -p $dest
			cp -r src $dest/brush-sizes-docker/
            cp -r brush-sizes-docker.desktop $dest/
          '';
        };
      });

      # Dev shell: Krita plus symlinks so edits show up after a Krita restart
      devShells = forAll (pkgs: {
        default = pkgs.mkShell {
          packages = [
            (pkgs.python3.withPackages (ps: [ ps.pyqt5 ps.pyqt6 ]))
            pkgs.pyright
          ];
          shellHook = ''
            target="''${XDG_DATA_HOME:-$HOME/.local/share}/krita/pykrita"
            mkdir -p "$target"
            ln -sfn "$PWD/src" "$target/brush-sizes-docker"
            ln -sfn "$PWD/brush-sizes-docker.desktop" "$target/brush-sizes-docker.desktop"
            echo "Linked plugin into $target"
            echo "Run 'krita', then enable it under Settings → Configure Krita → Python Plugin Manager (one-time)."
          '';
        };
      });
    };
}

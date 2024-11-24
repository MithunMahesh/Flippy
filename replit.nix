{ pkgs }: {
  deps = [
    pkgs.libopus                # Required for audio (used by Lavalink)
    pkgs.ffmpeg-full            # Required for audio (used by Lavalink)
    pkgs.gdb                    # Debugging tool
    pkgs.replitPackages.prybar-python310  # Replit's Python 3.10 runtime
    pkgs.replitPackages.stderred # Error formatting for Replit
    pkgs.python310Full          # Python 3.10 (Full version)
    pkgs.python310Packages.pip  # Pip for Python 3.10
  ];
}

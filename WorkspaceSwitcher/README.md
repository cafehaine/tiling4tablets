# WorkspaceSwitcher

WorkspaceSwitcher will be a fullscreen app that shows in a grid all the open
Sway workspaces.

The grid will contain a "preview" of the workspace, which will consist of the
icon of the app tiled/stacked according to the contents of the workspace.

The icon will be determined by the window's app\_id (see the xdg-shell wayland
protocol), or if the app is an X11 app, then the app's class will be used. Then
we simply look for a desktop entry with the matching name.

For example, a simple tiled workspace with firefox (represented by `F`s) and
gimp (represented by `G`s) will have the following preview:

```
+----+----+
| FF | GG |
| FF | GG |
+----+----+
```

If a container is tiled or stacked, show the focused one on top, then the next
one beneath it.
Here Firefox is stacked on top of Gimp:

```
+-----+
| FFG |
| FFG |
+-----+
```

# symlinker
Python script that creates symbolic links.

Below is an example that will grab all files that have a png extension and create symbolic links in a new folder
"png_images".

```python
./symlink -b /home/user/.../images -t *.png -d /home/user/.../png_images --recursive
```



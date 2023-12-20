# RatCam - Capture
This is package used for capturing images of rats on the Jetson Nanoe, which can be later processed by ratcam-process.

## Setup
### Prerequisits
1. Connect camera into CAM0 CSI slot on the Jetson. (Ensure the metal connectors on ribbon cable are facing the heatsink).
2. Ensure ext4 formated USB or storage is connected into the Jetson. Ideally above 64GB to store enough footage.
3. Ensure USB storage is automatically mounted to a location on boot.

### Flash
Install latest [JetPack 4.6.4 3](https://developer.nvidia.com/jetpack-sdk-464) (L4T 2.7.4) as per usual.

### Drivers
At the time of write, the v3 camera (with the Sony X708 sensor) is not supported on the official L4T drivers. The default CSI sensor is IMX219. It is possible to use IMX477 using [Jetson-IO](https://docs.nvidia.com/jetson/archives/l4t-archived/l4t-3273/index.html#page/Tegra%20Linux%20Driver%20Package%20Development%20Guide/hw_setup_jetson_io.html#wwpID0E02D0HA).

Plugging in the CSI connector and rebooting gives an error in dmesg saying `board setup failed`
```
dmesg | grep -i imx
```

For more details on supported sensors, look up [here](https://developer.nvidia.com/embedded/jetson-partner-supported-cameras?t-1_supported-jetson-products=nano).

Fortunately RidgeRun provides the drivers for the IMX708 sensor:
1. Access Jetson (Either ssh or plugin monitor, keyboard and mouse)
2. [Download the .deb package](https://drive.google.com/drive/folders/1sjrnHeHoEOkBxllWu4qS8ElnJGoTAWyN) and copy to the Jetson filesystem
2. Install the Debian package to the Jetson:
    ```
    sudo dpkg -i --force-overwrite ./nano.deb
    ```
3. Enable the device tree changes, by editting `/boot/extlinux/extlinux.conf` file and set contents to:
    ```
    TIMEOUT 30
    DEFAULT Develop

    MENU TITLE L4T boot options

    LABEL primary
        MENU LABEL primary kernel
        LINUX /boot/Image
        FDT /boot/dtb/kernel_tegra210-p3448-0003-p3542-0000.dtb
        INITRD /boot/initrd
        APPEND ${cbootargs} quiet root=/dev/mmcblk0p1 rw rootwait rootfstype=ext4 console=ttyS0,115200n8 console=tty0 fbcon=map:0 net.ifnames=0 nv-auto-config
    ```
4. Reboot the Jetson:
    ```
    sudo reboot
    ```
5. Verify drivers work by capturing image:
    ```
    gst-launch-1.0 nvarguscamerasrc num-buffers=1 sensor_id=0 ! 'video/x-raw(memory:NVMM), width=4608, height=2592, framerate=14/1, format=NV12' ! nvjpegenc ! filesink location=test_image.jpg
    ```
For more details, follow the instruction on [ridgerun.com](https://developer.ridgerun.com/wiki/index.php/Raspberry_Pi_Camera_Module_3_IMX708_Linux_driver_for_Jetson#Installing_the_Driver_-_Option_A:_Debian_Packages_(Recommended))

### Install Software

sudo apt install libcairo2-dev libgirepository1.0-dev

gst-launch-1.0 nvarguscamerasrc sensor_id=0 -e ! 'video/x-raw(memory:NVMM),width=4608,height=2592,framerate=14/1, format=NV12' ! nvvidconv ! 'video/x-raw,width=1920,height=1080' ! x264enc ! qtmux ! filesink location=RidgeRun_out.mp4

## Run
To begin aquiring images:
```
TODO
```
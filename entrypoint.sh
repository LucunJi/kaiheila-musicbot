# credits https://askubuntu.com/questions/1338747/virtual-audio-sink-virtual-audio-cable-on-ubuntu

# Load pulseaudio virtual audio source
pulseaudio -D --exit-idle-time=-1

sleep 5

pactl load-module module-null-sink sink_name=vspeaker sink_properties=device.description=virtual_speaker
pactl load-module module-remap-source master=vspeaker.monitor source_name=vmic source_properties=device.description=virtual_mic
pactl set-default-sink vspeaker
pactl set-default-source vmic

# Start Selenium-Chrome-Standalone
/opt/bin/entry_point.sh

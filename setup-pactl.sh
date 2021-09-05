pulseaudio -D
sleep 5
pactl load-module module-null-sink sink_name=vspeaker sink_properties=device.description=virtual_speaker
pactl load-module module-remap-source master=vspeaker.monitor source_name=vmic source_properties=device.description=virtual_mic
pactl set-default-sink vspeaker
pactl set-default-source vmic
echo "all the sources"
pactl list short sources
echo ""
echo "all the sinks"
pactl list short sinks

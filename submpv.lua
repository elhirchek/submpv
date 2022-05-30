-- submpv lua script
-- ===================|

local python_path = '' -- path to python bin
local submpv_path = '' -- path to submpv.py script 

-- Log function: log to both terminal and MPV OSD (On-Screen Display)
function log(string,secs)
	secs = secs or 2.5
	mp.msg.warn(string)
	mp.osd_message(string,secs)
end

-- download/load function
function submpv()
	log('search for arabic subtitle!')
	local utils = require 'mp.utils'
	--get directory and filename
	local d,f = utils.split_path(mp.get_property('path'))
	-- run command and capture stdout
	local openPop = assert(io.popen(..python_path..''..submpv_path..' -d '.. d ..' \''..f..'\'', 'r')) -- path to script
	local output = openPop:read('*a')
	openPop:close()
	-- check stdout 
	if string.find(output, 'done') then
		log('Arabic subtitles ready!')
		-- to make sure all downloaded subtitle loaded
		mp.set_property('sub-auto', 'all')
		mp.commandv('rescan_external_files','reselect')
	else
		log('Arabic subtitles not found!')
	end
end
mp.add_key_binding('/','submpv',submpv)

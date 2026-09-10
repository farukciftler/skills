-- sheet_to_aseprite.lua — uca-sheet/1 (PNG + JSON) -> .aseprite with one TAG per animation,
-- per-frame durations, loop flags and "event:<Function>" cel user data. Unity's 2D Aseprite Importer
-- (com.unity.2d.aseprite, Import Mode = Animated Sprite) then generates the clips + events by itself.
-- Requires Aseprite >= 1.3 (json global, tag.repeats).
--   aseprite -b --script-param sheet=Ranger_sheet.png --script-param meta=Ranger_sheet.json \
--               --script-param out=Ranger.aseprite --script sheet_to_aseprite.lua
local p = app.params
assert(p.sheet and p.meta and p.out, "need --script-param sheet=, meta=, out=")
local fh = assert(io.open(p.meta, "r"))
local meta = json.decode(fh:read("a"))
fh:close()
assert(meta.schema == "uca-sheet/1", "not a uca-sheet/1 file")
local sheet = Image{ fromFile = p.sheet }
local W, H = meta.frameWidth, meta.frameHeight
local spr = Sprite(W, H, ColorMode.RGB)
local layer = spr.layers[1]
layer.name = meta.name
local count = 0
app.transaction(function()
  for _, a in ipairs(meta.animations) do
    local first = count + 1
    for i, fr in ipairs(a.frames) do
      local frame = (count == 0) and spr.frames[1] or spr:newEmptyFrame()
      count = count + 1
      frame.duration = fr.durationMs / 1000.0
      local img = Image(W, H, ColorMode.RGB)
      img:drawImage(sheet, Point(-fr.x, -fr.y))
      local cel = spr:newCel(layer, frame, img, Point(0, 0))
      for _, e in ipairs(a.events or {}) do
        if e.frame == i - 1 then cel.data = "event:" .. e["function"] end
      end
    end
    local tag = spr:newTag(first, count)
    tag.name = a.name
    tag.repeats = a.loop and 0 or 1   -- 0 = infinite; the Unity importer treats >=1 as non-looping
  end
end)
spr:saveAs(p.out)
print(string.format("wrote %s: %d frames, %d tags", p.out, count, #spr.tags))

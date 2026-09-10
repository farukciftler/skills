# Storyboarding & Cutscenes for 2D Side-View Games

## Contents
1. What a game storyboard is for
2. Cutscene budget and the interactivity ladder
3. 2D screen grammar
4. Camera language in a side view
5. Acting with small sprites
6. Pipeline: beat sheet → thumbnails → panel spec → animatic
7. Panel spec format
8. Drawing SVG thumbnails (when asked)
9. Gameplay storyboards (level moments, not cutscenes)
10. Checklist

---

## 1. Purpose

A storyboard is a cheap way to find out if a scene works before anyone animates it. In games it serves two jobs:
- **Cutscene boards** — shot-by-shot plans for non-interactive or semi-interactive scenes.
- **Gameplay boards** — key frames of what the player sees and does in a set-piece (a chase, a reveal, a boss intro), including what they control.

Film pipeline, adapted: script breakdown → thumbnails → detailed panels → animatic (panels on a timeline with scratch audio/text to test timing) → revisions. For games, the animatic step is best done **in-engine** with placeholder sprites.

## 2. Cutscene budget and the interactivity ladder

Default to the least control-taking option that still lands the beat (see `flow-and-pacing.md` §9). For a 3–6 hour platformer:
- **Full cutscenes:** 3–5 in the whole game (opening, midpoint, fall, climax, ending).
- **Semi-interactive scenes:** player can walk or look while the scene plays (walk-and-talk, camera hold with control).
- **Scripted level events:** the world acts while the player plays (a bridge collapses behind them, a figure watches from the background).

Every full cutscene: skippable on repeat, checkpoint after, under ~60 s unless it's the ending.

## 3. 2D screen grammar

In side-view games, direction is meaning. The player learns it in minutes, so use it deliberately:

| Direction | Default meaning | Use to… |
|---|---|---|
| Left → right | progress, forward, future | normal advancement |
| Right → left | retreat, return, past, going home | backtracking arcs, flashbacks, fleeing |
| Upward | aspiration, effort, escape | climbing stories, hope |
| Downward | descent, danger, the unconscious, truth | descent-and-return spines |
| Toward camera (foreground) | intimacy, threat approaching | a character stepping close |
| Into background | distance, mystery, the unreachable | the goal glimpsed far away |

Break the rule on purpose: a chapter where "forward" is suddenly leftward tells the player something changed without a word.

**Screen-direction continuity (180° rule, 2D version):** if a character is walking right in one shot, keep them facing right in the next unless you show the turn. Flipping direction between shots reads as "they turned around".

## 4. Camera language in a side view

Most 2D games have one camera: a side view that can **pan, zoom, hold, shake, and frame**. That's enough.

| Move | Effect | Notes |
|---|---|---|
| Zoom out (wide) | isolation, scale, awe, "look how far" | reveal the goal or the size of the threat |
| Zoom in (tight) | intimacy, emotion, a detail matters | use during a conversation's key line |
| Camera hold (stops following) | "something is here", time to look | player keeps control; great for background events |
| Camera lead (ahead of player) | anticipation, speed | chases and escapes |
| Camera lag (behind) | reluctance, heaviness | tired or grieving character |
| Pan away from player | the world matters more than you right now | reveals, background story events |
| Shake | impact, threat | sparingly; offer reduce-motion setting |
| Letterbox bars | "a scene is happening" | clear signal of control loss; remove instantly on return |
| Parallax layers | depth, world beyond reach | background layer = story layer (Inside tells half its story there) |

**Framing:** place the character on the rule-of-thirds line facing into open space (lead room). Put them against the edge facing out and the frame feels trapped.

## 5. Acting with small sprites

At 16–64 px tall, faces barely read. Emotion lives in:
- **Posture:** slump, straighten, lean in, step back.
- **Timing:** a pause before responding is a line of dialogue.
- **Idle animations:** a nervous character fidgets; a confident one stands still.
- **Movement speed:** walking slower after bad news.
- **Distance between characters:** they move apart during an argument, closer at reconciliation. Board this explicitly.
- **Looking:** who looks at whom, and who looks away.
Playdead's work shows how much subtle changes in the protagonist's movement can carry dread, fear or excitement.

## 6. Pipeline

1. **Beat sheet:** list the beats of the scene in plain sentences. One beat = one change (in information, emotion, or power).
2. **Thumbnails:** tiny rough frames, one per beat, just silhouettes and arrows. Solve staging here.
3. **Panel spec:** fill the template (§7) for each surviving thumbnail.
4. **Script lock:** final lines only after staging works. Staging often lets you delete lines.
5. **In-engine animatic:** greybox level, placeholder sprites, timed text bubbles, scratch music. Play it. Time it. Cut 20%.
6. **Review with a fresh player:** can they retell what happened? Did they feel the beat?

## 7. Panel spec format

Use `assets/storyboard-panel-template.md`. Each panel:

```
PANEL 03 | Scene: 4-END "The Rope" | Duration: 3.5s | Control: player can walk (no jump)
FRAME: zoom 1.2x, camera holds at tile (84, 12); Mira at left third facing right, Teo at right third facing away
SCREEN DIRECTION: Mira moving right (toward Teo); Teo static
ACTION: Teo coils the rope slowly; stops when Mira arrives
TEXT: TEO: "He took the good rope." (bubble above Teo, 1 bubble)
AUDIO: wind loop fades to 40%; single low piano note on bubble appear
TRANSITION: cut to PANEL 04 on text advance
NOTES: distance between them = 3 tiles; closes to 1 tile by PANEL 06
```

## 8. SVG thumbnails

When the user wants visuals, draw simple SVG thumbnails: a 16:9 frame, ground line, silhouettes (rounded rects/circles), arrows for movement, a small bubble for text, a label with the panel number. Keep them schematic. Don't draw real copyrighted characters; use the user's own characters as simple shapes. Group 3–6 panels in one SVG strip.

## 9. Gameplay storyboards

For set-pieces (chase, collapse, boss intro), board what the **player** sees and does:
- Panel per decision point, not per second.
- Mark the input the player needs ("jump here", "dash through").
- Mark where the camera leads or holds.
- Mark failure → respawn point.
- Mark the single audio/visual cue that makes the next hazard readable.

## 10. Checklist

- [ ] Could this be done without taking control? If yes, why aren't we?
- [ ] Screen direction consistent (or broken on purpose)?
- [ ] Does distance between characters change across the scene?
- [ ] Can the scene be understood with all text removed?
- [ ] Is there a checkpoint after it and is it skippable on repeat?
- [ ] Is the first gameplay moment after the scene safe (player re-orients)?
- [ ] Animatic timed and cut by ~20%?

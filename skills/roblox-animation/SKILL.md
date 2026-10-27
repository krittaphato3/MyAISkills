---
name: roblox-animation
description: >-
  Handles Roblox character and object animation: R15 rig setup, Animator and AnimationTrack playback,
  priority layers, blended transitions, animation markers, IKControl, in-place locomotion, and
  cutscene camera work. Use when animating a character, NPC, weapon, door, or cinematic, or when
  animation fails to play, blend, or replicate. UI motion belongs to roblox-ui-ux; tweened VFX to
  roblox-vfx.
metadata:
  version: 1.0.0
  domain: roblox
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: roblox-animator
---

# Roblox Animation

Animation in Roblox is not "play a clip". It is a small state machine on top of a rig, with priority
layers deciding who wins, markers synchronizing feedback, and the server owning what other players
see. Most broken animations are one of four things: no `Animator` on the server, wrong priority,
a track that was never loaded, or the clip trying to move the character through the world.

## WHEN TO USE

- Character locomotion, attacks, emotes, hit reactions, deaths, idles.
- NPC or creature animation driven by AI state.
- Moving props: doors, platforms, weapons, machines (rig-based, not physics).
- Cutscenes and camera sequences involving characters.
- "The animation doesn't play / doesn't blend / only plays for one player".

## WHEN NOT TO USE

- Property tweening for UI — `roblox-ui-ux`.
- Physics-driven movement (constraints, motors, conveyor) — `roblox-scripting` + engine constraints.
- Particle/beam effects attached to a rig — `roblox-vfx`.
- Importing meshes or rigging a custom body mesh — `roblox-assets` (then come back for the clips).
- Non-Roblox engines — `game-developer`.

## DECISION TREE

```text
1. WHAT IS BEING ANIMATED?
   Player/NPC character → R15 rig + Animator + AnimationTracks
   Prop/mechanism        → AnimationController + Animator on the model, or TweenService for simple
   Camera only           → camera CFrame tweens (pattern 4), no rig needed

2. WHERE DOES THE ANIMATOR LIVE?
   Anything other players must see → create the Animator on the SERVER (server-owned Humanoid).
   Purely local first-person flourishes → client Animator is acceptable, but it will not replicate.

3. WHAT LAYERS EXIST?
   Idle < Movement < Action < Action2 < Action3 < Action4.
   Locomotion on Movement, attacks/abilities on Action*, hit reactions on Action2/3.
   One owner per layer per moment; blend with weights/fades rather than hard stops.

4. HOW DOES IT START AND STOP?
   Load once, cache the track, play/stop explicitly; never LoadAnimation per attack.
   On state change: fade out the previous layer, fade in the next, adjust speed for locomotion.
   Disconnect marker connections and stop tracks when the character dies/despawns.

5. WHAT SYNCHRONIZES TO THE CLIP?
   Impact sound, hit VFX, damage window → animation markers (`GetMarkerReachedSignal`).
   Gameplay authority stays on the server; markers fire presentation on each client, and the server
   validates damage separately (never trust a client marker as a hit).

6. DOES IT MOVE THE CHARACTER?
   No — Roblox avatar animation is in-place. Locomotion, dashes, and root displacement are gameplay
   code (server-authoritative). A clip that translates the root will snap back or desync.
```

## PATTERNS

### 1. Server-owned animator + cached tracks
```lua
-- server: one Animator per character, created once
local humanoid = character:WaitForChild("Humanoid")
local animator = humanoid:FindFirstChildOfClass("Animator") or Instance.new("Animator", humanoid)

local tracks = {}
local function getTrack(animId: string): AnimationTrack
    if not tracks[animId] then
        local anim = Instance.new("Animation")
        anim.AnimationId = animId
        tracks[animId] = animator:LoadAnimation(anim)
    end
    return tracks[animId]
end
```

### 2. Layered state machine
```lua
local function playAction(animId: string, fadeIn: number)
    local track = getTrack(animId)
    track.Priority = Enum.AnimationPriority.Action
    track:Play(fadeIn or 0.1)
    return track
end

local function stopAction(track: AnimationTrack)
    track:Stop(0.15)
end
```
Keep one active action track per layer; stopping the wrong one is how limbs freeze mid-swing.

### 3. Markers for feedback (not authority)
```lua
local track = playAction(ATTACK_ID, 0.08)
local conn
conn = track:GetMarkerReachedSignal("Hit"):Connect(function()
    Effects:PlayHit(character)          -- local presentation
    -- damage is applied by the server's own timed logic, not by this client marker
end)
track.Stopped:Once(function() conn:Disconnect() end)
```
Name markers in the editor (`Hit`, `Footstep`, `Cast`, `End`) and keep the names stable — scripts
depend on them.

### 4. Camera and cutscene sequencing
```lua
local cam = workspace.CurrentCamera
local original = cam.CameraType
cam.CameraType = Enum.CameraType.Scriptable
local tween = TweenService:Create(cam, TweenInfo.new(2.5, Enum.EasingStyle.Sine), {CFrame = shotCFrame})
tween:Play(); tween.Completed:Wait()
cam.CameraType = original
```
Lock input during a cutscene (`ContextActionService`), restore it on every exit path including
errors, and never chain `Completed:Wait()` without a timeout/cleanup.

### 5. IK for adaptation
```lua
local ik = Instance.new("IKControl")
ik.Type = Enum.IKControlType.Position
ik.ChainRoot = character.UpperTorso
ik.EndEffector = character.RightHand
ik.Target = targetAttachment
ik.Weight = 1
ik.Parent = character.Humanoid
```
Use IK for reaching, aiming, and foot placement on uneven ground; disable it when the state ends or
it will fight the next clip.

### 6. Locomotion that feels right without root motion
- Drive movement in gameplay code; scale the walk/run track speed to actual velocity.
- Blend idle↔walk↔run by weight, not by hard switching.
- Match foot phase to speed loosely; perfect foot-lock is not worth the complexity on Roblox.
- Jump/fall clips on `Movement` layer, triggered by Humanoid state changes.

## FAILURE MODES & MITIGATIONS

1. **Animation plays locally only** — Animator created on the client. *DETECT:* other players see the
   default pose. *FIX:* server-owned Animator on the character.
2. **Track never loads** — `LoadAnimation` called on a Humanoid without an Animator, or with an
   invalid asset id. *DETECT:* silent no-op. *FIX:* ensure Animator, pcall the load, log failures.
3. **Wrong priority** — idle overrides the attack. *DETECT:* the action never visibly plays. *FIX:*
   explicit priority per layer; one owner per layer.
4. **Repeated LoadAnimation** — new track per attack, leaked connections. *DETECT:* memory growth,
   overlapping plays. *FIX:* cache tracks (pattern 1).
5. **Root motion** — clip translates the rig, character snaps back. *DETECT:* slide-then-reset.
   *FIX:* author in place; move via code.
6. **Stuck in cutscene** — input never restored on error. *DETECT:* player cannot move after a scene.
   *FIX:* restore in a single cleanup path with pcall.
7. **Marker spam** — marker used as damage authority. *DETECT:* exploiters trigger hits. *FIX:*
   server-side damage windows; markers are presentation only.
8. **IK fighting clips** — IKControl left enabled. *DETECT:* limbs drift after the action. *FIX:*
   destroy/disable IK when leaving the state.

## QUANTITATIVE RULES

- Animation Editor runs at 30 fps; author timing against that.
- Priority order: `Action4 > Action3 > Action2 > Action > Movement > Idle > Core`.
- One Animator per Humanoid; one active track per priority layer.
- Cache every AnimationTrack; zero `LoadAnimation` calls in combat loops.
- Fade times: 0.05–0.15 s for actions, 0.2–0.3 s for locomotion blends.
- Cutscene input lock must be restored on every exit path; verify in a playtest.
- No root translation in avatar clips; movement is gameplay code.

## VERIFICATION GATE

- [ ] Animator exists on the server for anything replicated.
- [ ] Tracks loaded once and cached; no per-action reload.
- [ ] Priorities assigned per layer; no layer has two owners at once.
- [ ] Playtested with two clients: both see the same animation.
- [ ] Markers drive presentation only; damage/state validated server-side.
- [ ] Locomotion is in-place; movement comes from gameplay code.
- [ ] Cutscene exits restore camera and input (tested via an early exit).
- [ ] Console clean; no leaked connections after 10 attack cycles.

## REFERENCES

- `roblox-assets` — rigging and mesh import for custom characters
- `roblox-scripting` — server authority, state machines, damage windows
- `roblox-vfx` — effects attached to animation markers
- `roblox-ui-ux` — UI motion and cutscene overlays
- `roblox-studio-mcp` — playtest and capture animation states
- Roblox docs: Animator, AnimationTrack, Animation Editor, IKControl, character specifications

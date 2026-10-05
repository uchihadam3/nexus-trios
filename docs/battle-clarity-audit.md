# Battle clarity and iconography

## Audit of the existing interface

- The large circular ring reads `Fighter.action` (0–1). The engine advances it by `STEP × speed / character.interval`; Haste, Slow, Rooted, and Paralyzed affect this rate. The presentation fills it continuously and flashes an `↑` or `↓` cue when a `shift` effect changes that value.
- The three ability tiles read `Fighter.skills[i]`: `charge` fills from event rules and time, `cooldown` blocks charge, `executing` is the short visual execution window, and `Fighter.cast` tracks a preparing skill. Event based gains now emit a `charge` event with the skill index, source fighter, cause, and amount. Time gains remain smooth and quiet.
- A `shift` effect now emits a `tempo` event with source, target, and signed action progress. The portrait ring shows the direction and a brief reason cue.
- Status badges read `Fighter.statuses`: each has an ID, source, intensity, and remaining seconds. Duration refreshes retain their maximum display duration. There is no discrete stack-count field in the engine; intensity is not shown as a stack number. Positive states use a cool badge and upward mark; negative states use a warm badge and downward mark.
- Temporary battle cues are the director's `Beat.events`: synergy lines, status VFX, interruption marks, outcome chips, charge explanations, and the optional battle history. They are not persistent status or ability indicators.

## Ability art

The catalog contains 100 characters and 300 skills. Each skill has a separate transparent SVG at `public/assets/skills/<character-id>/<skill-slug>.svg`; all 300 paths and file contents are unique. The renderer selects a semantic line-art motif from skill names/descriptions and `Visual`, and gives each character/skill a deterministic palette and silhouette variation. The generated master SVG uses a 64×64 viewBox and scales to the actual 16–32 px interface sizes. `public/assets/skills/manifest.json` lists each exact character/skill path. The atlas is available in the development-only debug screen (`#debug`).

## Universal state set

These are the 14 states currently in the engine; the battle and help screens use one shared icon per state:

| ID | Label | Meaning |
|---|---|---|
| exposed | Exposto | Receives more damage. |
| paralyzed | Paralisado | Cannot act or advance preparation. |
| protected | Protegido | Reduces damage and resists interruption. |
| marked | Marcado | Receives additional damage and enemy attention. |
| slow | Lento | Action ring and preparation progress more slowly. |
| haste | Acelerado | Normal actions and preparation progress faster. |
| confused | Confuso | May miss a normal action and hit itself. |
| rooted | Preso | Slows actions and preparation. |
| regen | Regeneração | Restores Condition over time. |
| burning | Queimando | Loses Condition over time. |
| electric | Eletrificado | Receives additional damage. |
| silenced | Silenciado | Cannot start skills; existing preparation continues. |
| strengthened | Fortalecido | Deals more damage. |
| weakened | Enfraquecido | Deals less damage. |

Tap an ability, state, character portrait, or character name during a battle to open the compact battle inspector. It translates charge triggers into plain Portuguese, reports current load/cooldown and state time, and names the applying fighter. The Normal/Detailed/Off setting controls transient charge notices; tapped explanations remain available.

## Verification

`tests/assets.test.ts` checks that all 300 character-specific assets exist, have unique paths/content, use no text/emoji, and match the character catalog. `tests/battle.test.ts` verifies that combat emits charge cause/source and action-tempo events. The development atlas presents the full 100×3 roster for visual review.

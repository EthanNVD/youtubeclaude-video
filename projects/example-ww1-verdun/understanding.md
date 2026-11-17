# Understanding — example: WW1, Verdun to the first tanks (2:04)

(This 2-minute excerpt comes from the film "What Was The REAL Turning Point of WW1?". The whole of `work/reading.md` was read before this file was written.)

## 1. The film in three lines
- **Question:** Why did 1916 fail to decide the war, even though both sides tried to win it with huge battles?
- **Answer:** Germany's plan to bleed France at Verdun bled Germany too. Brusilov and the Somme forced Germany to fight everywhere at once.
- **Era and sides:** WW1; Germany (and Austria-Hungary) vs France, Britain and Russia.

## 2. People
| cast id | preset | name on the name card | role on the name card | what they do in the story |
|---|---|---|---|---|
| falkenhayn | falkenhayn | General Erich von Falkenhayn | Chief of the German General Staff, 1914-16 | plans Verdun to bleed the French army |
| brusilov | brusilov | General Aleksei Brusilov | Russian South-Western Front | smashes the Austro-Hungarian armies in June 1916 |

## 3. Places and dates
| time | place | date |
|---|---|---|
| 0:00 | Western Front | end of 1915 |
| 0:34 | Verdun (on the Meuse) — in places.json | February 1916 |
| 1:15 | Lutsk / Galicia (eastern front) — in places.json | June 1916 |
| 1:31 | Romania (country) | 1916 |
| 1:34 | the Somme (Albert, Amiens) | 1 July 1916 |
| 1:59 | the Somme | September 1916 |

## 4. Numbers
- Verdun: about 300 days → **alone** → `label` on an action card.
- French 377,000 vs German 337,000 casualties (one estimate) → **compare** → `chart`.
- About 70,000 men a month → **alone** → `label` on the silhouette card.
- Somme, first day: 57,470 casualties → **alone** → `counter` on `stretcher`.
- Of these, 19,240 killed → **alone** → `counter` on `mg_nest`.
- Somme: 141 days → **alone** → `label`.

## 5. Chapters
| # | starts at | title | what happens in it | battle chapter? |
|---|---|---|---|---|
| 1 | 0:00 "By the end of 1915" | Bleeding | Falkenhayn's attrition plan, Verdun, Brusilov, the Somme, the first tanks | yes |

## 6. Beats (chapter 1)
```
0:00 | By the end of 1915          | deadlock on the Western Front, men under shellfire      | under_fire (british, dawn, END OF 1915)
0:04 | General Erich von Falkenhayn | Falkenhayn worries over a report                        | decision (worried, warroom, name card)
0:08 | Attacks on the Western Front | men go over the top and fall for nothing                | assault (british, 3 falls on "cost enormous")
0:14 | So he went looking           | Falkenhayn walks in at night and starts writing         | decision variant C (night, then write)
0:16 | According to the memoirs     | the line from his memoirs                               | document (3 s)
0:20 | his idea was that France     | the French line holds: no breakthrough possible         | trench_wait (french, lookout, label THE LINE HOLDS)
0:25 | if the French army could     | French reinforcements pour toward the front             | march (french, dusk, trucks)
0:28 | Pick a place the French      | German heavy guns firing                                | gun_crew (german, dusk, fire on "heavy guns")
0:34 | The place he picked was Verdun | where: Metz → Verdun, Paris → Verdun                  | map_move (≤ 5 s)
0:39 | The attack began in February | storm troops in the snow                                | wave (german, snow, dawn, 21 FEB 1916)
0:41 | It became the longest battle | French pinned in a shell hole for months                | under_fire (french, label ≈ 300 DAYS)
0:47 | And the arithmetic never worked | German attackers fall too                            | wave (german, left, 2 falls)
0:50 | One modern calculation       | the two casualty totals compared                         | chart
1:01 | That's roughly seventy thousand | grief over a long time                               | silhouette (stretcher bearers at dusk, label)
1:07 | The army that was supposed to bleed | one German soldier hit, comrade kneels           | hit (german)
1:11 | And while Verdun went on     | two new attacks: east and west                           | map_move (two arrows)
1:15 | In June, the Russian general | Brusilov orders the attack                               | decision (tent, point, name card)
1:19 | attacked on a wide front     | the Russian wave, Austrians break                        | wave (russian, enemy austrian)
1:25 | inflicting losses            | Austro-Hungarians surrender                              | surrender
1:26 | Germany had to send divisions east | troop trains leave                                 | rail
1:30 | and Romania was encouraged   | Romania joins the Allies                                 | map_locate (highlight Romania)
1:34 | Then, on the 1st of July     | British go over the top on the Somme                     | assault variant B (1 JULY 1916)
1:39 | On its first day             | the wounded carried back, counter 57,470                 | stretcher (counter)
1:45 | including nineteen thousand  | German MG crew firing, counter 19,240                    | mg_nest (counter)
1:49 | It's still the worst day     | the field after, a survivor walks back                   | aftermath (grey, label)
1:53 | But the battle went on       | rain and mud, 141 days                                   | trench_wait (rain, label)
1:56 | and the Germans facing it    | Germans under the British barrage                        | under_fire (german, trench)
1:59 | In September, the first tanks | Mark IV crawls in, Germans flee                         | tank_attack (SEPTEMBER 1916)
```
Checks:
- No recipe appears twice in a row.
- 20 of the 28 lines are action.
- Every "alone" number is on an action card.

## 7. Fact flags
- The casualty figures are "one modern calculation" and are labelled ONE ESTIMATE on screen.
- Falkenhayn's "bleed France" aim comes from his post-war memoirs. The document is titled "AS HE WROTE AFTER THE WAR".

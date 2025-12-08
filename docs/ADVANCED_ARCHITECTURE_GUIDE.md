# Advanced Architecture Guide

This document explains **architecture details** and **engine behavior** in *GuessNumberPygame*.

---

## 1. Architecture Patterns

### 1.1 ECS Architecture

The ECS approach here is small and intentionally simple.

#### Entities

* Every `GameObject` stores its components in a dictionary.
* There is no global registry of entities - each scene manages its own list.

#### Components

* Components hold **only data**, no logic.
* Some components store animation-related values (e.g., `AlphaComponent`), but do not perform any animations by themselves.

#### Systems

* Systems loop through **all entities in the scene** and check if they contain specific components.

#### ECS Limitations

* Component lookup is O(N) because entities are stored in a list.
* Systems are executed in a fixed order - there is no system scheduler.
* Components cannot be queried globally across scenes.

This is fine for a small game, but something to consider when reusing the engine.

---

### 1.2 Service Locator Pattern Usage

The Service Locator is used only for stable, global services:

* `app` (GameApp)
* `sound_system`
* configuration

Notes:

* The Service Locator **does not manage lifecycles** - nothing is cleaned up automatically.
* It should not store game state; only long-lived services belong here.

---

### 1.3 Event Bus System Architecture

The EventBus provides simple decoupled messaging.

* Events run **synchronously** - no queueing.
* There is no hierarchy or namespacing - event names are plain strings.
* There is no type checking.

---

## 2. Code Flow and System Architecture

### 2.1 Main Application Flow

```text
main.py
  → GameApp(config)
        → initialize pygame, systems, and services
  → GameApp.run()
        → game loop:
              - read input events
              - convert coordinates (for scaling)
              - send events to current scene
              - scene.update
              - systems update entities
              - render to a virtual surface
              - scale and blit to the window
````

#### Additional Details

* **Event order matters**:
  `MOUSEBUTTONDOWN` sets `.pressed`,
  but only `MOUSEBUTTONUP` can trigger `.on_click()`.
* Scene transitions happen **after** the main loop frame using fade-out callbacks.

---

### 2.2 Scene Lifecycle

* `enter()` and `exit()` are wrapped in try/except so errors do not crash the app.
* Each scene has its own entity list - switching scenes replaces the entire entity set.
* Fade-out animations work by adjusting `AlphaComponent.target_alpha`, and the render system animates the change.

This creates a smooth visual transition.

---

## 3. Advanced Features and Implementations

### 3.1 Responsive Design - Internal Scaling Model

The game always renders at **fixed 640×400**, regardless of window size.

#### Virtual Surface

* All drawing happens on a hidden 640×400 surface.
* The final image is scaled to the actual window.

#### Aspect Ratio

`ResponsiveScaleManager` calculates:

* a uniform `scale` factor
* `offset_x` / `offset_y` for letterboxing

#### Mouse Input Scaling

* Mouse coordinates are converted back into virtual space **before** any UI logic is processed.
* UI never needs to know the real window size.

This makes the UI simple and predictable.

---

### 3.2 Button Press Animation System

#### Press Rules

* On `MOUSEBUTTONDOWN`, the button becomes `pressed = True`.
* On `MOUSEBUTTONUP`, we trigger `.on_click()` **only if**:

  1. the button was previously pressed
  2. the cursor is still inside the button

#### Rendering

* A pressed button is drawn 2 pixels lower, creating a “push” effect.

#### Images Inside Buttons

If a button also has an `ImageComponent`:

* The image moves with the button.
* Shadows and highlight effects also respond to the pressed state.

This gives a soft and tactile UI feel.

---

### 3.3 Input System

* The system manages focus for input fields.
* It keeps track of press → release consistency even when the cursor moves.
* Hover state updates every frame, not only on mouse events.

---

### 3.4 Render System

#### Rendering Order

1. Draw button shadow
2. Apply press offset
3. Draw button box
4. Draw highlight gradient
5. Draw text
6. Draw image (if any)
7. Apply alpha fading

#### AlphaComponent Animation

```python
alpha += animation_speed * dt * direction
```

Where `direction` depends on the `target_alpha`.

---

## 4. Performance Considerations and Optimization Paths

### 4.1 Identified Bottlenecks

#### Rendering & Input

* Both systems scan all entities → O(N).
* Component checks are repeated each frame.

#### ECS Design

* No component indexing.
* Entities are not pooled or recycled.

#### Scene Management

* Switching scenes creates new entity lists.
* No incremental updates.

---

### 4.2 Future Work

#### Component Indexing

Store entities with the same components together:

```python
component_pools[ButtonComponent]
component_pools[ImageComponent]
```

This would reduce scanning.

#### Render Graph

Introduce layers to:

* control draw order
* batch similar operations
* simplify special effects

#### Entity Lifecycle Manager

Add:

* deferred deletion
* pooling
* cleanup hooks

---

## 5. Best Practices

### 5.1 Configuration Management

* Pydantic validates complex fields (like colors).
* Environment variables override config values cleanly.
* Property getters maintain backward compatibility.

---

### 5.2 Error Handling Patterns

* Scene transitions are protected from exceptions.
* Missing assets do not break the game - fallbacks are used.
* UI elements degrade gracefully if something fails.
* Logging records issues without stopping the app.

import jax
from jax.lib import xla_bridge

print("--- Device Information ---")
print(f"Platform: {xla_bridge.get_backend().platform}")
print(f"Devices: {jax.devices()}")

# 실제 연산 장치 확인
import jax.numpy as jnp
x = jnp.arange(5)
print(f"Array location: {x.device()}")
from typing import Dict, Optional

def lookup_address(address: str, address_map: Dict[str, Dict]) -> Optional[Dict]:
    return address_map.get(address.lower().strip())

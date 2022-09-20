# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by 
# Wehrmacht and Luftwaffe, Nazi Germany. 
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.
 
from copy import deepcopy
from ctypes import ArgumentError

# Enigma Components
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WHEELS = {
    "I" : {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21
    }
}

UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],  # 휠 정보
    "WHEEL_POS": [],  # 현재 휠 위치
    "ETW": ETW,
    "PLUGBOARD": []
}


def apply_settings(ukw, wheel, wheel_pos, plugboard):
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))
    
    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)


# Enigma Logics Start

# Plugboard
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input


# ETW: entry disc
def pass_etw(input):
    return SETTINGS["ETW"][ord(input) - ord('A')]


# Wheels
def pass_wheels(input, reverse = False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order

    wheel_pos = SETTINGS["WHEEL_POS"]
    wheels = SETTINGS["WHEELS"]
    # 정방향이면
    if not reverse:
        # First rotor -> Second rotor -> Last rotor
        for wheel in range(2, -1, -1):
            input = ETW[(wheel_pos[wheel] + ETW.find(input)) % 26] if wheel == 2 \
                else ETW[(wheel_pos[wheel] + ETW.find(input) - wheel_pos[wheel + 1]) % 26]
            input = wheels[wheel]["wire"][ord(input) - ord('A')]

    # 역방향이면
    else:
        # Last rotor -> Second rotor -> First rotor
        for wheel in range(0, 3, 1):
            input = ETW[(wheel_pos[wheel] + ETW.find(input)) % 26] if wheel == 0 \
                else ETW[(wheel_pos[wheel] + ETW.find(input) - wheel_pos[wheel - 1]) % 26]
            input = ETW[wheels[wheel]["wire"].find(input)]

        # back to ETW
        input = ETW[(ETW.find(input) - wheel_pos[2]) % 26]

    return input


# UKW: reflector
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]


# Wheel Rotation
def rotate_wheels():
    # Implement Wheel Rotation Logics

    wheels = SETTINGS["WHEELS"]
    wheel_pos = SETTINGS["WHEEL_POS"]

    for wheel in range(2, -1, -1):
        # ETW 한바퀴 다 돌면 다시 A부터
        wheel_pos[wheel] = (wheel_pos[wheel] + 1) % 26

        # 노치에 걸리면 다음 로터를 한 칸씩 회전
        wheels[wheel]["turn"] -= 1
        if wheels[wheel]["turn"] >= 0:
            break
        else:
            wheels[wheel]["turn"] = 25


# Enigma Exec Start
# plaintext = input("Plaintext to Encode: ")  # 평문 입력
# ukw_select = input("Set Reflector (A, B, C): ")  # 반사판 설정
# wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
# wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
# plugboard_setup = input("Plugboard Setup: ")

plaintext = "MOONDAYEONMOONDAYEONMOONDAYEONMOONDAYEONMOONDAYEONMOONDAYEONMOONDAYEON"
ukw_select = "B"
wheel_select = "III II I"
wheel_pos_select = "A A A"
plugboard_setup = "MN"

apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)
answer = ""
for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse=True)
    encoded_ch = pass_plugboard(encoded_ch)

    print(encoded_ch, end='') # KLQACIUKFD FMQVXJPSAZ LIUVZDVLPX QJPTBGOSNG PTPQACMWGD FAUZMXEWKK CHIMQRTFCB
    answer += encoded_ch

print("\n")
print(answer == "KLQACIUKFDFMQVXJPSAZLIUVZDVLPXQJPTBGOSNGPTPQACMWGDFAUZMXEWKKCHIMQRTFCB")
# get answer from https://piotte13.github.io/enigma-cipher/

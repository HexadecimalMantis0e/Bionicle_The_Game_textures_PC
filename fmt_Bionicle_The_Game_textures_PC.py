from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Bionicle: The Game textures", ".bin")
    noesis.setHandlerTypeCheck(handle, btgCheckType)
    noesis.setHandlerLoadRGBA(handle, btgLoadRGBA)
    noesis.logPopup()
    return 1

def btgCheckType(data):
    return 1

def handleTexture(bitStream, texturePalette, textureType, textureWidth, textureHeight):
    if textureType == 0x18:
        texture = rapi.imageDecodeRawPal(bitStream.readBytes(textureWidth * textureHeight), texturePalette, textureWidth, textureHeight, 8, "b8g8r8")
    elif textureType == 0x20:
        texture = rapi.imageDecodeRawPal(bitStream.readBytes(textureWidth * textureHeight), texturePalette, textureWidth, textureHeight, 8, "b8g8r8a8")
    elif textureType == 0x00:
        texture = rapi.imageDecodeRaw(bitStream.readBytes(textureWidth * textureHeight * 0x04), textureWidth, textureHeight, "b8g8r8a8")

    texture = rapi.imageFlipRGBA32(texture, textureWidth, textureHeight, 0, 1)
    return texture

def btgLoadRGBA(data, texList):
    texCount = 0
    bs = NoeBitStream(data)
    fileSizeDiv4 = bs.getSize() // 4

    for i in range(0, fileSizeDiv4 - 1):
        temp = bs.readUInt()

        if temp == 0x00545C6C:
            address = bs.tell()
            texCount += 1
            width = bs.readUInt()
            height = bs.readUInt()
            bs.seek(0x08, NOESEEK_REL)
            texSize = bs.readUInt()
            bs.seek(0x0F, NOESEEK_REL)
            type = bs.readUByte()
            bs.seek(0x0A, NOESEEK_REL)
            print(texCount)
            print("Found a texture at " + str(hex(address - 0x04)) + ", width - " + str(width) + ", height - " + str(height))

            if type != 0x00:
                palSize = texSize - 0x12 - (width * height)
                pal = bs.readBytes(palSize)
            else:
                pal = None

            img = handleTexture(bs, pal, type, width, height)
            texList.append(NoeTexture(str(texCount), width, height, img, noesis.NOESISTEX_RGBA32))
            bs.seek(address, NOESEEK_ABS)
    return 1

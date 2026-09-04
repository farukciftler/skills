// grade.swift — Core Image ile GPU hızlandırmalı Moonstone renk düzeltmesi.
// Apple Silicon'da Metal üzerinden çalışır; ImageMagick kurulumuna gerek yoktur.
//
//   swift grade.swift <girdi> <cikti.jpg> [gece|gunduz|doku|notr] [yogunluk 0-1]
//
// Derleyip hızlandırmak için:  swiftc -O grade.swift -o grade   (~40x daha hızlı başlar)

import Foundation
import CoreImage
import CoreImage.CIFilterBuiltins

let args = CommandLine.arguments
guard args.count >= 3 else {
    print("kullanim: grade <girdi> <cikti.jpg> [gece|gunduz|doku|notr] [yogunluk]")
    exit(1)
}
let inURL  = URL(fileURLWithPath: args[1])
let outURL = URL(fileURLWithPath: args[2])
let look   = args.count > 3 ? args[3] : "gece"
let amount = args.count > 4 ? (Double(args[4]) ?? 1.0) : 1.0

guard var img = CIImage(contentsOf: inURL) else {
    FileHandle.standardError.write("girdi okunamadi: \(inURL.path)\n".data(using: .utf8)!)
    exit(1)
}

func mix(_ base: Double, _ target: Double) -> Double { base + (target - base) * amount }

// 1) Ton ve doygunluk
let cc = CIFilter.colorControls()
cc.inputImage = img
switch look {
case "gece":   cc.saturation = Float(mix(1.0, 0.86)); cc.brightness = Float(mix(0, -0.03)); cc.contrast = Float(mix(1.0, 1.10))
case "gunduz": cc.saturation = Float(mix(1.0, 1.04)); cc.brightness = Float(mix(0,  0.02)); cc.contrast = Float(mix(1.0, 1.04))
case "doku":   cc.saturation = Float(mix(1.0, 0.55)); cc.brightness = Float(mix(0, -0.01)); cc.contrast = Float(mix(1.0, 1.14))
default:       cc.saturation = 1.0; cc.brightness = 0; cc.contrast = 1.0
}
img = cc.outputImage ?? img

// 2) Beyaz dengesi — geceyi laciverte, gunduzu sicaga cek
if look != "notr" {
    let tp = CIFilter.temperatureAndTint()
    tp.inputImage = img
    tp.neutral = CIVector(x: 6500, y: 0)
    switch look {
    case "gece":   tp.targetNeutral = CIVector(x: CGFloat(mix(6500, 7400)), y: CGFloat(mix(0, -6)))
    case "gunduz": tp.targetNeutral = CIVector(x: CGFloat(mix(6500, 6100)), y: CGFloat(mix(0,  4)))
    case "doku":   tp.targetNeutral = CIVector(x: CGFloat(mix(6500, 6800)), y: CGFloat(mix(0, -3)))
    default: break
    }
    img = tp.outputImage ?? img
}

// 3) Golgeleri lacivert, parlak alanlari altin tarafa kaydir (split tone benzeri)
if look == "gece" || look == "doku" {
    let ci = CIFilter.colorPolynomial()
    ci.inputImage = img
    let s = amount
    // R: hafif azalt, B: golgeler icin hafif artir
    ci.redCoefficients   = CIVector(x: CGFloat(-0.010 * s), y: 1.0 + CGFloat(0.020 * s), z: 0, w: 0)
    ci.greenCoefficients = CIVector(x: CGFloat( 0.000 * s), y: 1.0,                       z: 0, w: 0)
    ci.blueCoefficients  = CIVector(x: CGFloat( 0.022 * s), y: 1.0 - CGFloat(0.030 * s), z: 0, w: 0)
    img = ci.outputImage ?? img
}

// 4) Cok hafif netlik
let sh = CIFilter.sharpenLuminance()
sh.inputImage = img
sh.sharpness = Float(0.35 * amount)
img = sh.outputImage ?? img

let ctx = CIContext(options: [.useSoftwareRenderer: false,
                              .workingColorSpace: CGColorSpace(name: CGColorSpace.extendedLinearSRGB)!])
let space = CGColorSpace(name: CGColorSpace.sRGB)!
do {
    if outURL.pathExtension.lowercased() == "png" {
        try ctx.writePNGRepresentation(of: img, to: outURL, format: .RGBA8, colorSpace: space)
    } else {
        try ctx.writeJPEGRepresentation(of: img, to: outURL, colorSpace: space,
                                        options: [kCGImageDestinationLossyCompressionQuality as CIImageRepresentationOption: 0.94])
    }
    print("\(outURL.lastPathComponent)  [\(look) x\(amount)]")
} catch {
    FileHandle.standardError.write("yazilamadi: \(error)\n".data(using: .utf8)!)
    exit(1)
}

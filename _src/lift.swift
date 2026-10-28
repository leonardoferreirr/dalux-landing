// Recorte de pessoa com o Vision da Apple (o mesmo "copiar sujeito" do iPhone).
// uso: swift tools/lift.swift entrada saida.png
import Foundation
import Vision
import CoreImage
import AppKit

let args = CommandLine.arguments
guard args.count >= 3, let src = NSImage(contentsOfFile: args[1]),
      let cg = src.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print("erro ao abrir"); exit(1) }
let handler = VNImageRequestHandler(cgImage: cg, options: [:])
let req = VNGenerateForegroundInstanceMaskRequest()
do {
  try handler.perform([req])
  guard let obs = req.results?.first else { print("nenhum sujeito"); exit(2) }
  let buf = try obs.generateMaskedImage(ofInstances: obs.allInstances, from: handler, croppedToInstancesExtent: false)
  let ci = CIImage(cvPixelBuffer: buf)
  let ctx = CIContext()
  guard let out = ctx.createCGImage(ci, from: ci.extent) else { exit(3) }
  let rep = NSBitmapImageRep(cgImage: out)
  try rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: args[2]))
  print(args[2], out.width, out.height, "instâncias:", obs.allInstances.count)
} catch { print("erro:", error); exit(4) }

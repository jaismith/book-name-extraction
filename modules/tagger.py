def tag(samples, start=0):
  labels = [None] * len(samples)

  i = start
  while i < len(samples):
    option = input('(CURRENT): "{}"\n\t(NEXT): "{}"\n[{} COMPLETE] (y) positive, (n) negative, (b) back, (m) merge, (q) quit: '.format(samples[i], samples[i + 1] if i < len(samples) - 1 else '', i))
    if option == 'y':
      labels[i] = True
    elif option == 'n':
      labels[i] = False
    elif option == 'b':
      i -= 2
    elif option == 'm' and i < len(samples) - 1:
      samples[i + 1] = '{} {}'.format(samples[i], samples[i + 1])
    elif option == 'q':
      break
    else:
      i -= 1

    print('\033[F\033[F\033[K\033[F\033[K\033[F\033[K')
    i += 1

  return labels

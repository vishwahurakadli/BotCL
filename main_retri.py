import os
import torch
from termcolor import colored
from configs import parser
from utils.engine_retri import train, test_MAP, test
from model.retrieval.model_main import MainModel
from loaders.get_loader import loader_generation


def main():
    model = MainModel(args)
    device = torch.device(args.device)

    # CUDNN
    torch.backends.cudnn.benchmark = True

    if not args.pre_train and args.dataset != "MNIST":
        checkpoint = torch.load(os.path.join(args.output_dir,
            f"{args.dataset}_{args.base_model}_cls{args.num_classes}_cpt_no_slot.pt"), map_location=device)
        model.load_state_dict(checkpoint, strict=False)
        # fix_parameter(model, ["slot"], mode="open")
        # print(colored('trainable parameter name: ', "blue"))
        # print_param(model)
        print("load pre-trained model finished, start training")
    else:
        print("start training")

    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(params, lr=args.lr)
    model.to(device)

    train_loader1, train_loader2, val_loader = loader_generation(args)

    for i in range(args.epoch):
        print(colored('Epoch %d/%d' % (i + 1, args.epoch), 'yellow'))
        print(colored('-' * 15, 'yellow'))

        # Adjust lr
        if i == args.lr_drop:
            print("Adjusted learning rate to 1/10")
            optimizer.param_groups[0]["lr"] = optimizer.param_groups[0]["lr"] * 0.1
        train(args, model, device, train_loader1, optimizer, i)
        if not args.pre_train and i % 5 == 0:
            map, acc = test_MAP(args, model, train_loader2, val_loader, device)
            print("acc: ", acc)
            print("map", map)

        if args.pre_train:
            test(args, model, val_loader, device)

        # if i == args.epoch - 1:
        torch.save(model.state_dict(), os.path.join(args.output_dir,
            f"{args.dataset}_{args.base_model}_cls{args.num_classes}_" + f"cpt{args.num_cpt if not args.pre_train else ''}_" +
            f"{'use_slot_' + args.act_type + '_' + args.cpt_activation if not args.pre_train else 'no_slot'}.pt"))


if __name__ == '__main__':
    args = parser.parse_args()
    main()